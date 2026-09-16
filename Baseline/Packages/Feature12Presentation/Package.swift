// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature12Presentation",
    products: [.library(name: "Feature12Presentation", targets: ["Feature12Presentation"])],
    dependencies: [.package(path: "../Feature12Domain"),
        .package(path: "../Feature12Data")],
    targets: [.target(name: "Feature12Presentation", dependencies: [.product(name: "Feature12Domain", package: "Feature12Domain"), .product(name: "Feature12Data", package: "Feature12Data")])]
)
