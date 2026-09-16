// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature06Presentation",
    products: [.library(name: "Feature06Presentation", targets: ["Feature06Presentation"])],
    dependencies: [.package(path: "../Feature06Domain"),
        .package(path: "../Feature06Data")],
    targets: [.target(name: "Feature06Presentation", dependencies: [.product(name: "Feature06Domain", package: "Feature06Domain"), .product(name: "Feature06Data", package: "Feature06Data")])]
)
