// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature10Presentation",
    products: [.library(name: "Feature10Presentation", targets: ["Feature10Presentation"])],
    dependencies: [.package(path: "../Feature10Domain"),
        .package(path: "../Feature10Data")],
    targets: [.target(name: "Feature10Presentation", dependencies: [.product(name: "Feature10Domain", package: "Feature10Domain"), .product(name: "Feature10Data", package: "Feature10Data")])]
)
