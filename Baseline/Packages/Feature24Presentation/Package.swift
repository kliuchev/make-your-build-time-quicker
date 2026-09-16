// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature24Presentation",
    products: [.library(name: "Feature24Presentation", targets: ["Feature24Presentation"])],
    dependencies: [.package(path: "../Feature24Domain"),
        .package(path: "../Feature24Data")],
    targets: [.target(name: "Feature24Presentation", dependencies: [.product(name: "Feature24Domain", package: "Feature24Domain"), .product(name: "Feature24Data", package: "Feature24Data")])]
)
