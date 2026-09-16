import Feature17Domain

public enum Feature17DataRepository {
    public static func load(_ id: Int) -> Feature17DomainModel {
        Feature17DomainModel(id: id, title: "Feature 17")
    }
}
